FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build-env
WORKDIR /src
COPY Whatsthis.API/*.csproj .
RUN dotnet restore
COPY Whatsthis.API .
RUN dotnet publish -c Release -o /publish

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /publish
COPY --from=build-env /publish .
EXPOSE 80
ENTRYPOINT ["dotnet", "Whatsthis.API.dll"]
