echo %1%
if "%1" == "" goto :error
echo ######## Comienza Personalidades ########
cd ./person
python person.py %1%
cd ..
echo ######## Comienza Stills ########
cd ./stills
python ./stills.py %1%
cd ..
echo ######## Comienza Cartel ########
cd ./cartel
python cartel.py %1% cartel.json
cd ..
echo ######## Continua Cartel ########
cd ./cartel
python cartel.py %1% car.json
cd ..
echo ######## Comienza Fotomontajes ########
python fotomontajes.py %1%
echo ######## Comienza FotoRodajes ########
python FotoRodajes.py %1%
echo ######## Comienza VhsDvd ########
cd ./vhs_dvd
python VhsDvd.py %1%


goto :end
:error
  echo No has introducido la contrasenia. Usage: script_total.bat <password>
:end
  echo Finalizado