pipeline {
    environment {
     PROJECT = "cbr-grabber"
     APP_NAME = "cbr-grabber"
     CLUSTER = "cbr-grabber"
     CLUSTER_ZONE = "europe-west3"
     IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
     JENKINS_CRED = "${PROJECT}"
     }

    agent {
    kubernetes {
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
      run: jnlp
spec:
  serviceAccountName: jenkins-admin
  containers:
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
  - name: python-39-slim
    image: python:3.9-slim-buster
    command:
    - cat
    tty: true
  - name: busybox
    image: busybox
    command:
    - cat
    tty: true
  - name: sonar-scanner
    image: newtmitch/sonar-scanner
    command:
    - cat
    tty: true
  - name: kubectl
    image: line/kubectl-kustomize:latest
    command:
    - cat
    tty: true
  - name: gcloud
    image: google/cloud-sdk:latest
    command:
    - cat
    tty: true
    volumeMounts:
      - name: kaniko-secret
        mountPath: /secret
    env:
      - name: GOOGLE_APPLICATION_CREDENTIALS
        value: /secret/kaniko-key.json
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: kaniko-secret
        mountPath: /secret
    env:
      - name: GOOGLE_APPLICATION_CREDENTIALS
        value: /secret/kaniko-key.json
  - name: kaniko-fe
    image: gcr.io/kaniko-project/executor:debug
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: kaniko-secret
        mountPath: /secret
    env:
      - name: GOOGLE_APPLICATION_CREDENTIALS
        value: /secret/kaniko-key.json
  volumes:
    - name: kaniko-secret
      secret:
        secretName: kaniko-secret
  imagePullSecrets:
  - name: jenkins-image-pull-secret

"""
   }
}
    stages {
        stage ('git clone - main') {
            when {
                branch 'main'
            }
            steps{
                container('git'){

                    git branch: 'main',
                        credentialsId: 'c65400e6-9ed8-422e-a033-7e6cc2c4d7c4',
                        url: 'https://github.com/Sacrament84/cbr-grabber.git'
                }
            }
        }
        stage ('git clone - dev') {
            when {
                branch 'dev'
            }
            steps{
                container('git'){
                    git branch: 'dev',
                        credentialsId: 'c65400e6-9ed8-422e-a033-7e6cc2c4d7c4',
                        url: 'https://github.com/Sacrament84/cbr-grabber.git'
                }
            }
        }
        stage('Sonarqube') {
             environment {
                sonar.projectKey=staging-cbr-grabbing:project
                sonar.sources=cbr-grabber
            }
            steps {
               dir('cbr-backend') {
                  container('sonar-scanner'){
                       withSonarQubeEnv('sonar-qube') {
                       sh "/bin/sonar-scanner"
                        }
                          timeout(time: 1	, unit: 'MINUTES') {
                          waitForQualityGate abortPipeline: true
                      }
                   }
                }
            }
        }
        stage ('building docker image backend - main') {
            when {
                branch 'main'
            }
            steps {
                dir ('cbr-backend') {
                    container('python-39-slim'){
                        sh 'python --version'
                    }
                    container(name: 'kaniko', shell: '/busybox/sh') {
                        sh 'pwd'
                        sh """
                        #!/busybox/sh
                        /kaniko/executor --dockerfile Dockerfile --context `pwd`/ --verbosity debug --insecure --skip-tls-verify --destination gcr.io/cbr-grabber/cbr-backend-prod/cbr-backend:$BUILD_NUMBER --destination gcr.io/cbr-grabber/cbr-backend-prod/cbr-backend:latest
                        """
                    }
                }
            }
        }
/*
        stage ('building docker image backend - dev') {
            when {
                branch 'dev'
            }
            steps {
                dir ('cbr-backend') {
                    container('python-39-slim'){
                        sh 'python --version'
                    }
                    container(name: 'kaniko', shell: '/busybox/sh') {
                        sh 'pwd'
                        sh """
                        #!/busybox/sh
                        /kaniko/executor --dockerfile Dockerfile --context `pwd`/ --verbosity debug --insecure --skip-tls-verify --destination gcr.io/cbr-grabber/cbr-backend-staging/cbr-backend:$BUILD_NUMBER --destination gcr.io/cbr-grabber/cbr-backend-staging/cbr-backend:latest
                        """
                    }
                }
            }
        }
        stage ('building docker image frontend - dev') {
            when {
                branch 'dev'
            }
            steps {
                dir ('cbr-frontend') {
                    container('python-39-slim'){
                        sh 'python --version'
                    }
                    container(name: 'kaniko-fe', shell: '/busybox/sh') {
                        sh 'pwd'
                        sh """
                        #!/busybox/sh
                        /kaniko/executor --dockerfile Dockerfile --context `pwd`/ --verbosity debug --insecure --skip-tls-verify --destination gcr.io/cbr-grabber/cbr-frontend-staging/cbr-frontend:$BUILD_NUMBER --destination gcr.io/cbr-grabber/cbr-frontend-staging/cbr-frontend:latest
                        """
                    }
                }
            }
        }
        stage ('building docker image frontend - prod') {
            when {
                branch 'main'
            }
            steps {
                dir ('cbr-frontend') {
                    container('python-39-slim'){
                        sh 'python --version'
                    }
                    container(name: 'kaniko-fe', shell: '/busybox/sh') {
                        sh 'pwd'
                        sh """
                        #!/busybox/sh
                        /kaniko/executor --dockerfile Dockerfile --context `pwd`/ --verbosity debug --insecure --skip-tls-verify --destination gcr.io/cbr-grabber/cbr-frontend-prod/cbr-frontend:$BUILD_NUMBER --destination gcr.io/cbr-grabber/cbr-frontend-prod/cbr-frontend:latest
                        """
                    }
                }
            }
        }
        stage ('deploy backend to k8s staging enviroment') {
            when {
                branch 'dev'
            }
            steps {
                dir ('cbr-backend/kustomize') {
                    container(name: 'kubectl') {
                        sh """
                               sed -ie "s#gcr.io/cbr-grabber/cbr-backend-staging:latest#gcr.io/cbr-grabber/cbr-backend-staging/cbr-backend:$BUILD_NUMBER#g" base/deployment.yaml
                               kubectl apply -k overlays/staging
                               kubectl rollout status deployment/staging-cbr-backend -n staging
                               kubectl get services -o wide -n staging
                           """

                    }
                }
            }
        }
        stage ('deploy frontend to k8s staging enviroment') {
            when {
                branch 'dev'
            }
            steps {
                dir ('cbr-frontend/kustomize') {
                    container(name: 'kubectl') {
                        sh """
                               sed -ie "s#gcr.io/cbr-grabber/cbr-frontend-staging:latest#gcr.io/cbr-grabber/cbr-frontend-staging/cbr-frontend:$BUILD_NUMBER#g" base/deployment.yaml
                               kubectl apply -k overlays/staging
                               kubectl rollout status deployment/staging-cbr-frontend -n staging
                               kubectl get services -o wide -n staging
                           """

                    }
                }
            }
        }
    }
}
*/
