# Using AI app and showing how Openteletry can help SRE's have one unique standard tool for observability that can be connected to any other provider

## here we see the example of `Jaeger` and `Prometheus` eporters
We will use docker to run those servers and maybe grafana dashboard to show metrics

## workflow is :
AI app > 
  integration of Opentelemetry > 
    span metrics of different providers > 
      provider exporter > 
        provider server...    > AI App : Logs, Metrics and Traces available >  maybe Grafana Dashboard
        other provider server > AI App : Logs, Metrics and Traces available > maybe grafana Dashboard

### install and play with it
```bash
# clone
git clone <this repo>
cd  <folder repo name>
# create virtual env
python3 -m venv <name_of_your_virtual_env>
source <name_of_your_virtual_env>/bin/activate
# install dependencies
pip install -r requirements.txt
```

After that you an add your own files or play with this boilerplate.
Maybe use a postgresql database to extend it... Interesting!
