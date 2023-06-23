#!/usr/bin/env bash

pipeline {

    agent {
        docker {
            image 'python3'
            args '-u root'
        }
    }

    stages {
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python3 ./Order/new_order.py'
            }
        }
    }
}