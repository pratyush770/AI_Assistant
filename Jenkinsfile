pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli
    command: ["cat"]
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true
    securityContext:
      runAsUser: 0
      readOnlyRootFilesystem: false
    env:
    - name: KUBECONFIG
      value: /kube/config
    volumeMounts:
    - name: kubeconfig-secret
      mountPath: /kube/config
      subPath: kubeconfig

  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
    volumeMounts:
    - name: docker-config
      mountPath: /etc/docker/daemon.json
      subPath: daemon.json

  volumes:
  - name: docker-config
    configMap:
      name: docker-daemon-config
  - name: kubeconfig-secret
    secret:
      secretName: kubeconfig-secret
'''
        }
    }

    environment {
        APP_NAME        = "ai-assistant"
        IMAGE_TAG       = "latest"
        REGISTRY_URL    = "nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085"
        REGISTRY_REPO   = "ai-assistant"
        SONAR_PROJECT   = "ai-assistant"
        SONAR_HOST_URL  = "http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000"
    }

    stages {

        // stage('Provide Streamlit Secrets') {
        //     steps {
        //         withCredentials([file(credentialsId: 'streamlit-secrets', variable: 'SECRET_FILE')]) {
        //             sh '''
        //                 mkdir -p .streamlit
        //                 cp "$SECRET_FILE" .streamlit/secrets.toml
        //             '''
        //         }
        //     }
        // }

        // stage('Build Docker Image') {
        //     steps {
        //         container('dind') {
        //             sh '''
        //                 echo ".streamlit/secrets.toml" > .dockerignore
        //                 sleep 15
        //                 docker build -t $APP_NAME:$IMAGE_TAG .
        //                 docker images
        //             '''
        //         }
        //     }
        // }

        // stage('SonarQube Analysis') {
        //     steps {
        //         container('sonar-scanner') {
        //             withCredentials([
        //                 usernamePassword(
        //                     credentialsId: 'sonar-token-2401121',
        //                     usernameVariable: 'SONAR_USER',
        //                     passwordVariable: 'SONAR_TOKEN'
        //                 )
        //             ]) {
        //                 sh '''
        //                     sonar-scanner \
        //                       -Dsonar.projectKey=$SONAR_PROJECT \
        //                       -Dsonar.host.url=$SONAR_HOST_URL \
        //                       -Dsonar.login=$SONAR_TOKEN \
        //                       -Dsonar.python.coverage.reportPaths=coverage.xml
        //                 '''
        //             }
        //         }
        //     }
        // }

        // stage('Login to Docker Registry') {
        //     steps {
        //         container('dind') {
        //             sh 'docker --version'
        //             sh 'sleep 10'
        //             sh 'docker login nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085 -u admin -p Changeme@2025'
        //         }
        //     }
        // }

        // stage('Build - Tag - Push Image') {
        //     steps {
        //         container('dind') {
        //             sh '''
        //                 docker tag $APP_NAME:$IMAGE_TAG \
        //                   $REGISTRY_URL/$REGISTRY_REPO/$APP_NAME:$IMAGE_TAG
        //
        //                 docker push $REGISTRY_URL/$REGISTRY_REPO/$APP_NAME:$IMAGE_TAG
        //                 docker pull $REGISTRY_URL/$REGISTRY_REPO/$APP_NAME:$IMAGE_TAG
        //                 docker images
        //             '''
        //         }
        //     }
        // }

        stage('Deploy Application') {
            steps {
                container('kubectl') {
                    dir('k8s-deployment') {
                        sh '''
                            # Ensure namespace exists
                            kubectl get namespace 2401121
                            kubectl describe pod ai-assistant-deployment-856b6c995-ps6fs -n 2401121
                            kubectl get pvc -n 2401121
                            # Apply Kubernetes manifests
                            // kubectl apply -f deployment.yaml
                            // kubectl apply -f service.yaml
                            // kubectl apply -f ingress.yaml

                            # Wait for deployment rollout
                            kubectl rollout status deployment/ai-assistant-deployment -n 2401121
                        '''
                    }
                }
            }
        }
    }
}
