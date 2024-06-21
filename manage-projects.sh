#!/bin/bash

# Array of project directories
projects=(
    "Year 1 (2021-2022)/COMP004 - Object-Oriented Programming/Notes App Coursework/"
    "Year 1 (2021-2022)/ENGF0002 - Design and Professional Skills CS/Scenario 2/djangoPermPostgres"
    "Year 2 (2022-2023)/COMP0016 - Systems Engineering/Group Portfolio/website"
    "Year 3 (2023-2024)/COMP0027 - Computer Graphics/UCL CG Renderer"
)

# Root directory
root=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Django secret key
export DJANGO_SECRET_KEY="_$4@nlrs73($elnuw8idm+r%#w7)k!jxcpy!9%n3aywjj^r2#!"

# Function to start or stop services for each project
operate_services() {
    local action=$1
    for project in "${projects[@]}"; do
        cd "$root/$project" || exit
        docker compose $action
    done
}

# Check the argument and call the function accordingly
if [ "$1" == "start" ]; then
    operate_services "up -d"
    docker run --rm -p 7681:7681 pythonshell
elif [ "$1" == "stop" ]; then
    operate_services "down"
    docker stop pythonshell
else
    echo "Usage: $0 [start|stop]"
    exit 1
fi

