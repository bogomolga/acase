#!/usr/bin/env groovy

pipeline {

    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'cd /usr/lib/python3.10 python ./Order/new_order.py'
            }
        }
    }
}