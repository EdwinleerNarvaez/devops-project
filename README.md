# DevOps Project — PIN Diplomatura

## Descripción
Pipeline CI/CD completo que integra Docker, GitHub Actions, Terraform, Snyk y Prometheus/Grafana.

## Tecnologías utilizadas
- **CI/CD:** GitHub Actions
- **Contenedores:** Docker + Docker Compose
- **IaC:** Terraform + AWS EC2
- **Seguridad:** Snyk + SBOM CycloneDX
- **Monitoreo:** Prometheus + Grafana

## Estructura del proyecto

devops-project/
├── .github/workflows/ci.yml # Pipeline CI/CD
├── app/
│ ├── app.py # App Flask
│ └── requirements.txt # Dependencias
├── terraform/
│ └── main.tf # Infraestructura AWS
├── docker-compose.yml # Orquestación local
├── prometheus.yml # Configuración Prometheus
└── Dockerfile # Imagen Docker


## Cómo ejecutar localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/EdwinleerNarvaez/devops-project.git
cd devops-project
```

### 2. Levantar todos los servicios
```bash
docker compose up -d
```

### 3. Acceder a los servicios
| Servicio | URL |
|----------|-----|
| App | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## Pipeline CI/CD
Cada push a `main` ejecuta automáticamente:
1. Build de imagen Docker
2. Test de la app
3. Escaneo de seguridad con Snyk
4. Generación de SBOM CycloneDX

## Infraestructura AWS
```bash
cd terraform
terraform init
terraform apply
```

## Monitoreo
- Prometheus recolecta métricas cada 15 segundos
- Grafana dashboard: Node Exporter Full (ID: 1860)
- Usuario Grafana: admin
