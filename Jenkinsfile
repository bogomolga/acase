#!/usr/bin/env bash

pipeline {
    agent {
         node {
          label 'Built-In' 
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
