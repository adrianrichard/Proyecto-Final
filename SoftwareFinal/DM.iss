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

[Dirs]
; Crear las carpetas incluso si están vacías
Name: "{app}\bd"; Permissions: users-modify
Name: "{app}\galeria"; Permissions: users-modify
Name: "{app}\informes"; Permissions: users-modify

[Files]
; Ejecutable principal
Source: "dist\DentalMatic.exe"; DestDir: "{app}"; Flags: ignoreversion

; Imágenes del directorio dist
Source: "dist\LOGO.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\LOGO11.png"; DestDir: "{app}"; Flags: ignoreversion

; Archivos de datos
Source: "imagenes\*"; DestDir: "{app}\imagenes"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "util\*"; DestDir: "{app}\util"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "bd\*"; DestDir: "{app}\bd"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "paginas\*"; DestDir: "{app}\paginas"; Flags: ignoreversion recursesubdirs createallsubdirs

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