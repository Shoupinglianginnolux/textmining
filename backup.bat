@ECHO OFF 
:: This batch file backups the current database with date.
TITLE Backup text mining database
ECHO Please wait... Checking system information.
for /f %%x in ('wmic path win32_utctime get /format:list ^| findstr "="') do set %%x
set today=%Year%-%Month%-%Day%
set ContainerID=92ab90256483
ECHO %ContainerID%
docker exec -ti %ContainerID% sh -c "mysqldump --all-databases --single-transaction --quick --lock-tables=false > full-backup-%today%.sql -u root -p 1234"
ECHO Finished mysqldump in the container %ContainerID%
docker cp %ContainerID%:/full-backup-%today%.sql D:\D\mysql_backup\
ECHO Finished copying backup file to local drive
PAUSE