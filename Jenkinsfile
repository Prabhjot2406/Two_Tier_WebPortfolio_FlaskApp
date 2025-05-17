pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '021891604768.dkr.ecr.us-east-1.amazonaws.com/flaskapp'
        IMAGE_TAG = 'latest'
        IMAGE_NAME = "${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {
        stage('Git Clone') {
            steps {
                echo 'Cloning the repository...'
                git url: "https://github.com/Prabhjot2406/Two_Tier_WebPortfolio_FlaskApp.git", branch: "main"
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds-id',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }
        stage('Pull Image') {
            steps {
                echo 'Pulling the Docker image from ECR...'
                sh 'docker pull $IMAGE_NAME'
                sh 'docker ps'
            }
        }
            stage('service down') {
        steps {
            echo 'Turn down running service'
            sh 'docker compose down --remove-orphans'
        }
    }

        stage('service up') {
            steps {
                echo 'Bringing service up'
                sh 'docker compose up -d --build'
            }
        }
        stage('Cleanup Docker') {
            steps {
                
                sh 'docker image prune -f'
            }
        }
    }
}

