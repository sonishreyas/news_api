#!/bin/bash

found=`ls venv`
if [[ $? == 0 ]];
then
      # The variable 'found' contains the full path where "myDirectory" is.
      # It may contain several lines if there are several folders named "myDirectory".
        echo "venv exists. sourcing venv/bin/activate"
else
    echo "creating venv"
    python3 -m venv venv
fi


source venv/bin/activate

flask run
