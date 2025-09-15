; installer.iss
; Script de instalación para DentalMatic

[Setup]
AppName=DentalMatic
AppVersion=1.0
AppPublisher=TuNombre
AppPublisherURL=https://www.tusitio.com
AppSupportURL=https://www.tusitio.com/support
AppUpdatesURL=https://www.tusitio.com/updates
DefaultDirName={pf}\DentalMatic
DefaultGroupName=DentalMatic
OutputDir=output
OutputBaseFilename=DentalMatic_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=imagenes\tooth.ico

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Ejecutable principal
Source: "DentalMatic.exe"; DestDir: "{app}"; Flags: ignoreversion

; Archivos de datos
Source: "imagenes\*"; DestDir: "{app}\imagenes"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "util\*"; DestDir: "{app}\util"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "informes\*"; DestDir: "{app}\informes"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "galeria\*"; DestDir: "{app}\galeria"; Flags: ignoreversion recursesubdirs createallsubdirs

; Incluir DLLs necesarias si existen

[Icons]
Name: "{group}\DentalMatic"; Filename: "{app}\DentalMatic.exe"; IconFilename: "{app}\imagenes\tooth.ico"
Name: "{group}\{cm:UninstallProgram,DentalMatic}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\DentalMatic"; Filename: "{app}\DentalMatic.exe"; Tasks: desktopicon; IconFilename: "{app}\imagenes\tooth.ico"

[Run]
Filename: "{app}\DentalMatic.exe"; Description: "{cm:LaunchProgram,DentalMatic}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
procedure InitializeWizard;
begin
  WizardForm.DirEdit.Text := ExpandConstant('{pf}') + '\DentalMatic';
end;