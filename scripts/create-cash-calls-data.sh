#!/bin/bash

python manage.py create_cashcalls

if [ $? -eq 0 ]; then
    echo "Cash call creation completed."
else
    echo "Cash Call creation failed."
    exit 1
fi

echo "Press any key to close this terminal..."
read -n 1 -s