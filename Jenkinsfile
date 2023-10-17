#!/usr/bin/env bash

pipeline {
    agent {
         node {
          label 'test_node' 
       }
    }
    stages {
        stage('Env install') {
            steps {
                echo 'Env installing...'
                sh 'pip install --no-cache-dir -r requirements.txt'
                }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python3 ./Order/new_order.py'
            }
        }
    }
}
