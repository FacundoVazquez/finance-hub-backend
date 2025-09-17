#!/bin/bash

PORT=8000

# Ejecutar PowerShell para buscar y matar procesos en ese puerto
powershell.exe -Command "
  \$ports = netstat -ano | findstr ':$PORT'
  if (\$ports) {
      \$ports | ForEach-Object {
          \$columns = (\$_ -split '\s+')
          \$procId = \$columns[-1]
          if (\$procId -ne '0') {
              Write-Output \"Matando proceso PID=\$procId en puerto $PORT\"
              taskkill /PID \$procId /F
          }
      }
  } else {
      Write-Output 'No hay procesos en ese puerto.'
  }
"
