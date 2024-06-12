# Log Instrumentation

## Deleting Original Logs

The current log instrumentation (Spring AOP) is suitable for the Spring Boot framework. If you wish to delete the original logs, you can use the following command:

```
python3 deleteLogs.py <web_application_path>
```

Then Instrument log with AOP intercepter: 
```
python3 Instrumentation.py <web application path>
```