#!/usr/bin/env groovy

pipeline {

    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python ./Order/new_order.py'
            }
        }
    }
}