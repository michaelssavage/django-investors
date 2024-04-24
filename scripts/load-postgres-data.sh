#!/bin/bash

python manage.py populate_data --path investor.csv --model investor

if [ $? -eq 0 ]; then
    echo "Done."
else
    echo "Investor data population failed."
    exit 1
fi

python manage.py populate_data --path investments.csv --model investment

if [ $? -eq 0 ]; then
    echo "Done."
else
    echo "Investments data population failed."
    exit 1
fi

echo "Data population completed."

echo "Press any key to close this terminal..."
read -n 1 -s