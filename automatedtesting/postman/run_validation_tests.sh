#!/bin/bash
newman run automatedtesting/postman/Validation_Test.postman_collection.json -e automatedtesting/postman/test_environment.json --reporters cli,junit --reporter-junit-export Results/ValidationTests.xml --suppress-exit-code --bail newman