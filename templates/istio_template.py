
TemplateExample = r"""

This template demonstrates the usage of Templite.

Within the defined delimiters we can write pure Python code:

${
def say_hello(name):
 write('Hello %s!' % name)
}$

And now we call the function: ${ say_hello('World') }$

Escaped starting delimiter: $\{
${ write('Escaped ending delimiter: }\$') }$

Also block statements are possible:
${x}$ is tempod
${ if svc == "frontend-dispatch": }$
x is greater than 10
${ :elif x > 5: }$
x is greater than 5
${ :else: }$
x is not greater than 5
${ :end-if / only the starting colon is essential to close a block }$
${ for i in range(x): }$
loop index is ${ i }$
${ :end-for }$
${ # this is a python comment }$
"""
TemplateGateway = r"""
kind: Gateway
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${gateway_name}$
  namespace: default
spec:
  servers:
    - hosts:
        - ${domain_9102}$
        - ${domain_9106}$
      port:
        name: http
        number: 80
        protocol: HTTP
  selector:
    istio: ingressgateway
"""
TemplatePrimaryFrontend = r"""
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ${svc}$
spec:
  host: ${svc}$
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
---
${ if svc == "frontend-dispatch": }$
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
    - ${domain_9106}$
  gateways:
    - ${gateway_name}$
    - mesh
  http: 
    - route:
        - destination:
            host: ${svc}$
            subset: v1

${ :else: }$
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
    - ${domain_9102}$
  gateways:
    - ${gateway_name}$
    - mesh
  http:
    - route:
        - destination:
            host: ${svc}$
            subset: v1
${ :end-if }$
"""

TemplateCanaryFrontend = r"""
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ${svc}$
spec:
  host: ${svc}$
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
---
${ if svc == "frontend-dispatch": }$
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
    - ${domain_9106}$
  gateways:
    - ${gateway_name}$
    - mesh
${ if header_type == "client_version": }$
  http: 
    - match:
    ${ for version in header_value: }$
        - headers:
            fullversion:
              exact: ${ version }$
    ${ :end-for }$
      route:
        - destination:
            host: frontend-dispatch
            subset: v2  
    - route:
        - destination:
            host: ${svc}$
            subset: v1
${ :elif header_type == "openid": }$
http: 
    - match:
        - headers:
            OpenId:
              regex: ${header_value}$
      route:
        - destination:
            host: frontend-dispatch
            subset: v2  
    - route:
        - destination:
            host: ${svc}$
            subset: v1
${ :else: }$
http: 
    - match:
        - headers:
            x-forwarded-for:
              exact: '182.150.28.60,10.33.17.248'
      route:
        - destination:
            host: frontend-dispatch
            subset: v2  
    - route:
        - destination:
            host: ${svc}$
            subset: v1
${ :end-if /header_type }$


${ :else: }$
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
    - ${domain_9102}$
  gateways:
    - ${gateway_name}$
    - mesh
  http:
    - route:
        - destination:
            host: ${svc}$
            subset: v1
${ :end-if }$
"""

TemplateCanaryBackend = r"""
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ${svc}$
spec:
  host: ${svc}$
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
---
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
  tcp:
     - match:
        - sourceLabels:
            version: v1
       route:
        - destination:
            host: ${svc}$
            subset: v1
     - match:
        - sourceLabels:
            version: v2
       route:
        - destination:
            host: ${svc}$
            subset: v2
"""
TemplatePrimaryBackend = r"""
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ${svc}$
spec:
  host: ${svc}$
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
---
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: ${svc}$
  namespace: default
spec:
  hosts:
    - ${svc}$
  tcp:
     - route:
        - destination:
            host: ${svc}$
            subset: v1
"""