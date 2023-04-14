FROM mcr.microsoft.com/dotnet/sdk:7.0 as build-env
WORKDIR /src
COPY Whatsthis.API/*.csproj .
RUN dotnet restore
COPY Whatsthis.API .
RUN dotnet publish -c Release -o /publish

FROM mcr.microsoft.com/dotnet/aspnet:7.0 as runtime
WORKDIR /publish
COPY --from=build-env /publish .
EXPOSE 80
ENTRYPOINT ["dotnet", "Whatsthis.API.dll"]
