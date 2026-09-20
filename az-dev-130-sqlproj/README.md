# az-dev-130-sqlproj

SDK-style SQL Database Project for Anchorline orders. Ships a DACPAC via GitHub Actions.

## Build

```
dotnet build -c Release
ls bin/Release/*/Anchorline.Orders.dacpac
```

## Deploy report (preview)

```
sqlpackage /Action:DeployReport \
    /SourceFile:bin/Release/netstandard2.1/Anchorline.Orders.dacpac \
    /TargetServerName:$ANCHORLINE_SQL_SERVER \
    /TargetDatabaseName:AnchorlineOrders \
    /UniversalAuthentication:True \
    /OutputPath:report.xml
```

## Publish

```
sqlpackage /Action:Publish \
    /SourceFile:bin/Release/netstandard2.1/Anchorline.Orders.dacpac \
    /TargetServerName:$ANCHORLINE_SQL_SERVER \
    /TargetDatabaseName:AnchorlineOrders \
    /UniversalAuthentication:True \
    /p:BlockOnPossibleDataLoss=True
```

## GitHub Actions workflow

`.github/workflows/sql-deploy.yml` runs the whole build → DeployReport → deploy-dev → gated deploy-prod pipeline.
