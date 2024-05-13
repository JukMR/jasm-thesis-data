#!/bin/bash

# Get all abstract python classes from a project folder

grep -oiR 'class.*ABC):' src/jasm
