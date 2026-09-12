pipeline {
    agent none

    stages {
        stage('Checkout') {
        agent any
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }
        stage('Test') {
            agent any
                docker {
                image 'python:3.11'
                args '-u root'
                }

            steps {
                echo 'Installing dependencies...'
                sh    'pip install --upgrade pip'
                sh    'pip install -r requirements.txt'

                echo 'Running tests...'
                sh 'pytest --html=report.html --self-contained-html --junitxml=test-result.xml'
            }
            post {
                always {
                    junit 'test-result.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report'
                    ])
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Pls check logs!'
        }
        always {
            cleanWs()
        }
    }
}