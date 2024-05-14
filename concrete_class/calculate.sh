#!/bin/bash

# Get all concrete python classes from a project folder filtering out abstract classes

grep -oiR 'class.*):' src/jasm | grep -v 'class.*ABC):'
