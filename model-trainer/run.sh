#!/bin/bash
echo "Changing Working Directory"
cd /mnt/c/"$3"/uploads
if [ $? -eq 0 ]; then
    echo OK
else
    echo "FAIL!!"
fi

# redirect stdout/stderr to a file
exec > "$1"/training.log 2>&1

echo "Creating Virtual Environment"
python3 -m venv env
if [ $? -eq 0 ]; then
    echo OK
else
    echo "FAIL!!"
    exit 1
fi
echo "Activating Environment"
activate () {
  . ./env/bin/activate
}
activate
if [ $? -eq 0 ]; then
    echo OK
else
    echo "FAIL!!"
    exit 1
fi

echo "Installing requirements from requirements.txt"
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo OK
else
    echo "FAIL!!"
    exit 1
fi
cd "$1"
echo "Executing $1/$2"
python3 "$2"
if [ $? -eq 0 ]; then
    echo OK
else
    echo "FAIL!!"
    exit 1
fi
echo "Training Successful!!"