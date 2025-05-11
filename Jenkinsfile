pipeline {
    
    agent any;
    stages {
        stage('code') {
            steps 
            {
                echo 'This is code stage'
                git url: "https://github.com/Prabhjot2406/Two_Tier_WebPortfolio_FlaskApp.git", branch: "main"
            }
        }
        stage('Build') {
            steps 
            {
                echo 'This is Build stage'
                sh "docker build -f Dockerfile_mini2 -t flaskapp_mini2 ."
            }
        }
        stage('Test') {
            steps {echo 'this is test stage'}
        }
        stage('Delpoy'){
            steps 
            {
                echo 'this is Deploy stage'
                sh "docker compose down && docker compose up -d --build"
            }
        }
    }
}
