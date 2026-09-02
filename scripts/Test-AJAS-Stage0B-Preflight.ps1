# =============================================================================
# RUN A READ-ONLY AJAS STAGE-0B PREFLIGHT.
# =============================================================================
& {
    $ajasRoot = 'C:\Users\steve\Documents\02_CODING\AJAS'
    $maximumDirectories = 500
    $auditIssueCodes = New-Object System.Collections.ArrayList
    $reviewReasonCodes = New-Object System.Collections.ArrayList
    $incompleteReasonCodes = New-Object System.Collections.ArrayList

    # =============================================================================
    # ADD A UNIQUE, SANITIZED RESULT CODE WITHOUT RECORDING PRIVATE PATHS.
    # =============================================================================
    function Add-UniqueCode {
        param(
            [Parameter(Mandatory = $true)]
            [System.Collections.ArrayList]$List,

            [Parameter(Mandatory = $true)]
            [string]$Code
        )

        if (-not $List.Contains($Code)) {
            [void]$List.Add($Code)
        }
    }

    # =============================================================================
    # NORMALIZE A WINDOWS PATH FOR CASE-INSENSITIVE CONTAINMENT COMPARISONS.
    # =============================================================================
    function ConvertTo-NormalizedPath {
        param([AllowNull()][string]$Path)

        if ([string]::IsNullOrWhiteSpace($Path)) {
            return $null
        }

        try {
            $expandedPath = [Environment]::ExpandEnvironmentVariables($Path)
            return [IO.Path]::GetFullPath($expandedPath).TrimEnd('\')
        }
        catch {
            Add-UniqueCode -List $auditIssueCodes -Code 'PATH_NORMALIZATION_FAILED'
            return $null
        }
    }

    # =============================================================================
    # TEST WHETHER ONE NORMALIZED PATH IS EQUAL TO OR BELOW ANOTHER.
    # =============================================================================
    function Test-PathWithin {
        param(
            [AllowNull()][string]$CandidatePath,
            [AllowNull()][string]$ParentPath
        )

        if ([string]::IsNullOrWhiteSpace($CandidatePath) -or [string]::IsNullOrWhiteSpace($ParentPath)) {
            return $false
        }

        if ([string]::Equals($CandidatePath, $ParentPath, [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }

        return $CandidatePath.StartsWith("$ParentPath\", [StringComparison]::OrdinalIgnoreCase)
    }

    # =============================================================================
    # CLASSIFY AN APPLICATION LOCATION WITHOUT PRINTING A USER OR ORGANIZATION PATH.
    # =============================================================================
    function Get-ApplicationLocationClass {
        param([Parameter(Mandatory = $true)][string]$ApplicationPath)

        $normalizedApplicationPath = ConvertTo-NormalizedPath -Path $ApplicationPath
        $normalizedUserProfile = ConvertTo-NormalizedPath -Path $env:USERPROFILE
        $normalizedProgramFiles = ConvertTo-NormalizedPath -Path $env:ProgramFiles
        $normalizedProgramFilesX86 = ConvertTo-NormalizedPath -Path ${env:ProgramFiles(x86)}
        $normalizedWindows = ConvertTo-NormalizedPath -Path $env:WINDIR

        if (Test-PathWithin -CandidatePath $normalizedApplicationPath -ParentPath $normalizedUserProfile) {
            return 'USER_PROFILE'
        }
        if ((Test-PathWithin -CandidatePath $normalizedApplicationPath -ParentPath $normalizedProgramFiles) -or
            (Test-PathWithin -CandidatePath $normalizedApplicationPath -ParentPath $normalizedProgramFilesX86)) {
            return 'PROGRAM_FILES'
        }
        if (Test-PathWithin -CandidatePath $normalizedApplicationPath -ParentPath $normalizedWindows) {
            return 'WINDOWS'
        }
        return 'OTHER'
    }

    # =============================================================================
    # PRINT START AND PLATFORM EVIDENCE.
    # =============================================================================
    Write-Output '===== BEGIN AJAS STAGE-0B READ-ONLY PREFLIGHT ====='
    Write-Output "AUDIT_UTC=$([DateTime]::UtcNow.ToString('o'))"
    Write-Output "POWERSHELL_VERSION=$($PSVersionTable.PSVersion.ToString())"
    Write-Output "POWERSHELL_EDITION=$($PSVersionTable.PSEdition)"
    Write-Output "OPERATING_SYSTEM=$([Environment]::OSVersion.VersionString)"

    # =============================================================================
    # REPORT ROOT STATUS AND REDIRECTION EVIDENCE WITHOUT DISCLOSING RAW PATHS.
    # =============================================================================
    $ajasRootExists = Test-Path -LiteralPath $ajasRoot -PathType Container
    Write-Output "AJAS_ROOT_EXISTS=$ajasRootExists"
    if (-not $ajasRootExists) {
        Add-UniqueCode -List $incompleteReasonCodes -Code 'AJAS_ROOT_NOT_FOUND'
    }

    $configuredDocumentsPath = $null
    try {
        $userShellFolderKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        $configuredDocumentsPath = (Get-ItemProperty -LiteralPath $userShellFolderKey -Name Personal -ErrorAction Stop).Personal
    }
    catch {
        Add-UniqueCode -List $auditIssueCodes -Code 'DOCUMENTS_CONFIGURATION_UNAVAILABLE'
        Add-UniqueCode -List $incompleteReasonCodes -Code 'DOCUMENTS_REDIRECTION_CHECK_INCOMPLETE'
    }

    $normalizedAjasRoot = ConvertTo-NormalizedPath -Path $ajasRoot
    $normalizedConfiguredDocuments = ConvertTo-NormalizedPath -Path $configuredDocumentsPath
    $normalizedDefaultDocuments = ConvertTo-NormalizedPath -Path (Join-Path -Path $env:USERPROFILE -ChildPath 'Documents')
    $documentsRedirected = $false
    if (($null -ne $normalizedConfiguredDocuments) -and ($null -ne $normalizedDefaultDocuments)) {
        $documentsRedirected = -not [string]::Equals(
            $normalizedConfiguredDocuments,
            $normalizedDefaultDocuments,
            [StringComparison]::OrdinalIgnoreCase
        )
    }

    $oneDrivePaths = @($env:OneDrive, $env:OneDriveConsumer, $env:OneDriveCommercial) |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { ConvertTo-NormalizedPath -Path $_ } |
        Where-Object { $null -ne $_ } |
        Select-Object -Unique
    $ajasUnderOneDrive = $false
    foreach ($oneDrivePath in $oneDrivePaths) {
        if (Test-PathWithin -CandidatePath $normalizedAjasRoot -ParentPath $oneDrivePath) {
            $ajasUnderOneDrive = $true
            break
        }
    }

    $ajasUnderConfiguredDocuments = Test-PathWithin `
        -CandidatePath $normalizedAjasRoot `
        -ParentPath $normalizedConfiguredDocuments
    Write-Output "DOCUMENTS_REDIRECTED=$documentsRedirected"
    Write-Output "AJAS_UNDER_CONFIGURED_DOCUMENTS=$ajasUnderConfiguredDocuments"
    Write-Output "ONEDRIVE_ENVIRONMENT_PRESENT=$($oneDrivePaths.Count -gt 0)"
    Write-Output "AJAS_UNDER_ONEDRIVE=$ajasUnderOneDrive"
    if ($documentsRedirected -or $ajasUnderOneDrive) {
        Add-UniqueCode -List $reviewReasonCodes -Code 'CLOUD_OR_REDIRECTED_DOCUMENTS_REVIEW_REQUIRED'
    }

    # =============================================================================
    # SEARCH AJAS AND ITS PARENTS FOR EITHER A .GIT FILE OR DIRECTORY.
    # =============================================================================
    $parentGitMarkerCount = 0
    $rootOrAncestorReparseCount = 0
    $currentPath = $normalizedAjasRoot
    $parentLevel = 0
    while (-not [string]::IsNullOrWhiteSpace($currentPath)) {
        try {
            if (Test-Path -LiteralPath $currentPath -ErrorAction Stop) {
                $currentPathItem = Get-Item -LiteralPath $currentPath -Force -ErrorAction Stop
                if ($currentPathItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    $rootOrAncestorReparseCount++
                }
            }
        }
        catch {
            Add-UniqueCode -List $auditIssueCodes -Code 'ROOT_OR_ANCESTOR_ACCESS_FAILED'
            Add-UniqueCode -List $incompleteReasonCodes -Code 'ROOT_TOPOLOGY_CHECK_INCOMPLETE'
        }

        $gitMarker = Join-Path -Path $currentPath -ChildPath '.git'
        try {
            $gitMarkerExists = Test-Path -LiteralPath $gitMarker -ErrorAction Stop
        }
        catch {
            $gitMarkerExists = $false
            Add-UniqueCode -List $auditIssueCodes -Code 'PARENT_GIT_MARKER_ACCESS_FAILED'
            Add-UniqueCode -List $incompleteReasonCodes -Code 'PARENT_GIT_CHECK_INCOMPLETE'
        }
        if ($gitMarkerExists) {
            try {
                $gitMarkerItem = Get-Item -LiteralPath $gitMarker -Force -ErrorAction Stop
            }
            catch {
                Add-UniqueCode -List $auditIssueCodes -Code 'PARENT_GIT_MARKER_ACCESS_FAILED'
                Add-UniqueCode -List $incompleteReasonCodes -Code 'PARENT_GIT_CHECK_INCOMPLETE'
                $gitMarkerItem = $null
            }
            $markerType = if (($null -ne $gitMarkerItem) -and $gitMarkerItem.PSIsContainer) { 'DIRECTORY' } else { 'FILE_OR_UNAVAILABLE' }
            $markerScope = if ($parentLevel -eq 0) { 'AJAS_ROOT' } else { "PARENT_$parentLevel" }
            Write-Output "GIT_MARKER_SCOPE=$markerScope|TYPE=$markerType"
            $parentGitMarkerCount++
        }

        $parentPath = Split-Path -Path $currentPath -Parent
        if ([string]::IsNullOrWhiteSpace($parentPath) -or ($parentPath -eq $currentPath)) {
            break
        }
        $currentPath = $parentPath
        $parentLevel++
    }
    Write-Output "PARENT_GIT_MARKER_COUNT=$parentGitMarkerCount"
    Write-Output "ROOT_OR_ANCESTOR_REPARSE_COUNT=$rootOrAncestorReparseCount"
    if ($parentGitMarkerCount -gt 0) {
        Add-UniqueCode -List $reviewReasonCodes -Code 'PARENT_OR_ROOT_GIT_MARKER_FOUND'
    }
    if ($rootOrAncestorReparseCount -gt 0) {
        Add-UniqueCode -List $auditIssueCodes -Code 'ROOT_OR_ANCESTOR_REPARSE_POINT_FOUND'
        Add-UniqueCode -List $incompleteReasonCodes -Code 'ROOT_TOPOLOGY_REQUIRES_REVIEW'
    }

    # =============================================================================
    # BOUNDEDLY SEARCH FOR NESTED .GIT FILES AND DIRECTORIES WITHOUT FOLLOWING
    # REPARSE POINTS.
    # =============================================================================
    $nestedGitMarkers = New-Object System.Collections.ArrayList
    $directoriesScanned = 0
    $directoryLimitReached = $false
    $reparseDirectoriesSkipped = 0
    if ($ajasRootExists -and $rootOrAncestorReparseCount -eq 0) {
        $directoryQueue = New-Object 'System.Collections.Generic.Queue[string]'
        $directoryQueue.Enqueue($normalizedAjasRoot)

        while ($directoryQueue.Count -gt 0) {
            if ($directoriesScanned -ge $maximumDirectories) {
                $directoryLimitReached = $true
                break
            }

            $directoryPath = $directoryQueue.Dequeue()
            $directoriesScanned++
            try {
                $children = @(Get-ChildItem -LiteralPath $directoryPath -Force -ErrorAction Stop)
            }
            catch {
                Add-UniqueCode -List $auditIssueCodes -Code 'NESTED_GIT_DIRECTORY_ENUMERATION_FAILED'
                Add-UniqueCode -List $incompleteReasonCodes -Code 'NESTED_GIT_CHECK_INCOMPLETE'
                continue
            }

            foreach ($child in $children) {
                if ($child.Name -eq '.git') {
                    if (-not [string]::Equals($directoryPath, $normalizedAjasRoot, [StringComparison]::OrdinalIgnoreCase)) {
                        $relativeParent = $directoryPath.Substring($normalizedAjasRoot.Length).TrimStart('\')
                        $markerType = if ($child.PSIsContainer) { 'DIRECTORY' } else { 'FILE' }
                        [void]$nestedGitMarkers.Add("$relativeParent|TYPE=$markerType")
                    }
                    continue
                }

                if ($child.PSIsContainer) {
                    if ($child.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                        $reparseDirectoriesSkipped++
                    }
                    else {
                        $directoryQueue.Enqueue($child.FullName)
                    }
                }
            }
        }
    }
    elseif ($ajasRootExists) {
        Add-UniqueCode -List $incompleteReasonCodes -Code 'NESTED_GIT_CHECK_INCOMPLETE'
    }

    if ($directoryLimitReached) {
        Add-UniqueCode -List $auditIssueCodes -Code 'DIRECTORY_LIMIT_REACHED'
        Add-UniqueCode -List $incompleteReasonCodes -Code 'NESTED_GIT_CHECK_INCOMPLETE'
    }
    if ($reparseDirectoriesSkipped -gt 0) {
        Add-UniqueCode -List $auditIssueCodes -Code 'REPARSE_DIRECTORY_SKIPPED'
        Add-UniqueCode -List $incompleteReasonCodes -Code 'NESTED_GIT_CHECK_INCOMPLETE'
    }
    Write-Output "DIRECTORIES_SCANNED=$directoriesScanned"
    Write-Output "DIRECTORY_LIMIT=$maximumDirectories"
    Write-Output "DIRECTORY_LIMIT_REACHED=$directoryLimitReached"
    Write-Output "REPARSE_DIRECTORIES_SKIPPED=$reparseDirectoriesSkipped"
    Write-Output "NESTED_GIT_MARKER_COUNT=$($nestedGitMarkers.Count)"
    foreach ($nestedGitMarker in $nestedGitMarkers) {
        Write-Output "NESTED_GIT_MARKER=$nestedGitMarker"
    }
    if ($nestedGitMarkers.Count -gt 0) {
        Add-UniqueCode -List $reviewReasonCodes -Code 'NESTED_GIT_MARKER_FOUND'
    }

    # =============================================================================
    # DISPLAY EXECUTION POLICIES WITHOUT CHANGING THEM.
    # =============================================================================
    try {
        foreach ($executionPolicy in Get-ExecutionPolicy -List -ErrorAction Stop) {
            Write-Output "EXECUTION_POLICY_$($executionPolicy.Scope.ToString().ToUpperInvariant())=$($executionPolicy.ExecutionPolicy)"
        }
    }
    catch {
        Add-UniqueCode -List $auditIssueCodes -Code 'EXECUTION_POLICY_CHECK_UNAVAILABLE'
    }

    # =============================================================================
    # DISPLAY ONLY FREE SPACE ON THE AJAS DRIVE.
    # =============================================================================
    try {
        $ajasDriveName = (Split-Path -Path $ajasRoot -Qualifier).TrimEnd(':')
        $ajasDrive = Get-PSDrive -Name $ajasDriveName -ErrorAction Stop
        Write-Output "AJAS_DRIVE=$($ajasDrive.Name)"
        Write-Output "AJAS_DRIVE_FREE_BYTES=$($ajasDrive.Free)"
    }
    catch {
        Add-UniqueCode -List $auditIssueCodes -Code 'DRIVE_SPACE_CHECK_UNAVAILABLE'
        Add-UniqueCode -List $incompleteReasonCodes -Code 'DRIVE_SPACE_CHECK_INCOMPLETE'
    }

    # =============================================================================
    # DISPLAY BITLOCKER STATUS WHEN AVAILABLE WITHOUT CHANGING IT.
    # =============================================================================
    $bitLockerCommand = Get-Command -Name Get-BitLockerVolume -CommandType Function, Cmdlet -ErrorAction SilentlyContinue
    if ($null -eq $bitLockerCommand) {
        Write-Output 'BITLOCKER_STATUS=COMMAND_NOT_AVAILABLE'
        Add-UniqueCode -List $auditIssueCodes -Code 'BITLOCKER_COMMAND_NOT_AVAILABLE'
    }
    else {
        try {
            $bitLockerVolume = Get-BitLockerVolume -MountPoint "${ajasDriveName}:" -ErrorAction Stop
            Write-Output "BITLOCKER_VOLUME_STATUS=$($bitLockerVolume.VolumeStatus)"
            Write-Output "BITLOCKER_PROTECTION_STATUS=$($bitLockerVolume.ProtectionStatus)"
            Write-Output "BITLOCKER_ENCRYPTION_METHOD=$($bitLockerVolume.EncryptionMethod)"
        }
        catch {
            Write-Output 'BITLOCKER_STATUS=UNAVAILABLE'
            Add-UniqueCode -List $auditIssueCodes -Code 'BITLOCKER_CHECK_UNAVAILABLE'
        }
    }

    # =============================================================================
    # REPORT APPLICATION AVAILABILITY AND A SANITIZED LOCATION CLASS WITHOUT
    # RUNNING THE APPLICATIONS.
    # =============================================================================
    $applicationNames = @('git.exe', 'node.exe', 'npm.cmd', 'python.exe', 'openssl.exe', 'curl.exe', 'docker.exe')
    foreach ($applicationName in $applicationNames) {
        $application = Get-Command -Name $applicationName -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($null -eq $application) {
            Write-Output "APPLICATION=$applicationName|NOT_FOUND"
        }
        else {
            $locationClass = Get-ApplicationLocationClass -ApplicationPath $application.Source
            Write-Output "APPLICATION=$applicationName|AVAILABLE|LOCATION_CLASS=$locationClass"
        }
    }

    # =============================================================================
    # REPORT POSTGRESQL INSTALLATION AND SERVICE METADATA WITHOUT EXECUTING OR
    # CONTROLLING POSTGRESQL.
    # =============================================================================
    try {
        $postgresqlBins = @(
            Get-Item -Path 'C:\Program Files\PostgreSQL\*\bin' -Force -ErrorAction Stop |
                Where-Object { $_.PSIsContainer }
        )
        Write-Output "POSTGRESQL_BIN_COUNT=$($postgresqlBins.Count)"
        foreach ($postgresqlBin in $postgresqlBins) {
            Write-Output "POSTGRESQL_VERSION_DIRECTORY=$($postgresqlBin.Parent.Name)"
        }
    }
    catch [System.Management.Automation.ItemNotFoundException] {
        Write-Output 'POSTGRESQL_BIN_COUNT=0'
    }
    catch {
        Write-Output 'POSTGRESQL_BIN_COUNT=UNAVAILABLE'
        Add-UniqueCode -List $auditIssueCodes -Code 'POSTGRESQL_DIRECTORY_CHECK_UNAVAILABLE'
    }

    try {
        $postgresqlServices = @(Get-Service -Name 'postgresql*' -ErrorAction Stop)
        Write-Output "POSTGRESQL_SERVICE_COUNT=$($postgresqlServices.Count)"
        foreach ($postgresqlService in $postgresqlServices) {
            Write-Output "POSTGRESQL_SERVICE=$($postgresqlService.Name)|STATUS=$($postgresqlService.Status)|START_TYPE=$($postgresqlService.StartType)"
        }
    }
    catch [Microsoft.PowerShell.Commands.ServiceCommandException] {
        Write-Output 'POSTGRESQL_SERVICE_COUNT=0'
    }
    catch {
        Write-Output 'POSTGRESQL_SERVICE_COUNT=UNAVAILABLE'
        Add-UniqueCode -List $auditIssueCodes -Code 'POSTGRESQL_SERVICE_CHECK_UNAVAILABLE'
    }

    # =============================================================================
    # EMIT A DETERMINISTIC, NON-CLAIMING RESULT.
    # =============================================================================
    $preflightResult = 'COMPLETE_NO_AUTOMATIC_BLOCKER_FOUND'
    if ($incompleteReasonCodes.Count -gt 0) {
        $preflightResult = 'INCOMPLETE'
    }
    elseif ($reviewReasonCodes.Count -gt 0 -or $auditIssueCodes.Count -gt 0) {
        $preflightResult = 'REVIEW_REQUIRED'
    }

    Write-Output "AUDIT_ISSUE_COUNT=$($auditIssueCodes.Count)"
    foreach ($auditIssueCode in $auditIssueCodes) {
        Write-Output "AUDIT_ISSUE_CODE=$auditIssueCode"
    }
    foreach ($reviewReasonCode in $reviewReasonCodes) {
        Write-Output "REVIEW_REASON_CODE=$reviewReasonCode"
    }
    foreach ($incompleteReasonCode in $incompleteReasonCodes) {
        Write-Output "INCOMPLETE_REASON_CODE=$incompleteReasonCode"
    }
    Write-Output "PREFLIGHT_RESULT=$preflightResult"
    Write-Output 'AJAS_TARGET_FILES_CREATED=0'
    Write-Output 'AJAS_TARGET_FILES_MODIFIED=0'
    Write-Output 'AJAS_TARGET_FILES_DELETED=0'
    Write-Output 'SOFTWARE_INSTALLED=0'
    Write-Output 'GIT_INITIALIZED=False'
    Write-Output 'EXPLICIT_NETWORK_COMMANDS_OR_API_CALLS=0'
    Write-Output '===== END AJAS STAGE-0B READ-ONLY PREFLIGHT ====='
}
