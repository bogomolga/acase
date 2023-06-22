#!/usr/bin/env python3

pipeline {

    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python3 ./Order/new_order.py'
            }
        }
    }
}