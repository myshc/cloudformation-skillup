# Simple CloudFormation
* VPC
* 2 subnets
* 2 web-instances 
* 1 jenkins instance
* 1 RDS instance
* 1 ALB
* Route53
* ACM attached to ALB

*NOTE:*
```
The root.yaml tamplate may be outdated!
Not using that template at the moment. Left it as an example.

I deployed the infrastructure without nested stacks in this order:
1. vpc.yaml
2. security.yaml
3. web-servers.yaml
4. alb.yaml
5. route53.yaml
6. database.yaml
7. jenkins.yaml
```
