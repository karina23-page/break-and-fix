pipeline {

    agent any

    environment {

        IMAGE_NAME = "tprff2301/movie-app"
        IMAGE_TAG = "${BUILD_NUMBER}"

        K3S_HOST = ""
    }

    stages {

        stage('Build') {

            steps {

                sh '''
                docker build \
                -t $IMAGE_NAME:$IMAGE_TAG \
                .
                '''
            }
        }

        stage('Push') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'movie-docker-token-id',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''

                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
                    --password-stdin

                    docker push \
                    $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy') {

            steps {

                sshagent(
                    credentials: ['movie-ec2-key']
                ) {

                    sh '''

                    ssh \
                    -o StrictHostKeyChecking=no \
                    ubuntu@$K3S_HOST "

                    sudo kubectl set image \
                    deployment/movie-app \
                    movie-app=$IMAGE_NAME:$IMAGE_TAG \
                    -n movie-space

                    sudo kubectl rollout status \
                    deployment/movie-app \
                    -n movie-space

                    sudo kubectl get pods \
                    -n movie-space
                    "
                    '''
                }
            }
        }
    }

    post {

        always {

            sh '''

            docker image prune -af || true

            '''
        }
    }
}