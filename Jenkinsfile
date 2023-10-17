#!/usr/bin/env bash

pipeline {
    agent {
         node {
          label 'TestNode' 
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
