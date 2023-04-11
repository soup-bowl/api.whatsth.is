using System.Net;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Distributed;
using WhatsthisAPI.Models;
using WhatsthisAPI.Service;
using Newtonsoft.Json;

namespace WhatsthisAPI.Controllers
{
	[ApiController]
	[Route("[controller]")]
	public class InspectController : ControllerBase
	{
		private readonly IDistributedCache _cache;
		private readonly IConfigurationService _configService;

		public InspectController(IDistributedCache cache, IConfigurationService configService)
		{
			_cache = cache;
			_configService = configService;
		}

		/// <summary>
		/// Inspect Site
		/// </summary>
		/// <remarks>
		/// The specified URL will be in-turn called by the system. The system will then perform various inspections on
		/// the response data and the connection to calculate what technology the website is running. In certain
		/// conditions, if the site is detected to be using a known REST API, useful data will also be harvested from
		/// their endpoint.
		///
		/// This is request-intensive, and results in a slow repsonse currently. To counter this, a caching engine is
		/// used to serve repeat requests with the same data.
		/// </remarks>
		[HttpGet("/inspect/{url}")]
		[ProducesResponseType(typeof(InspectionData), StatusCodes.Status200OK)]
		[ProducesResponseType(typeof(string), StatusCodes.Status503ServiceUnavailable)]
		public async Task<ActionResult<string>> Inspect(string url)
		{
			string decodedUrl = WebUtility.UrlDecode(url);
			string cleanUrl = Regex.Replace(decodedUrl, @"^(?!https?://)(\S+)$", "https://$1");
			string key = $"inspection-{cleanUrl}";

			try
			{
				string? cachedResult = await _cache.GetStringAsync(key);
				if (cachedResult != null)
				{
					InspectionData result = JsonConvert.DeserializeObject<InspectionData>(cachedResult)!;
					return new JsonResult(result);
				}

				IInspectionService inspection = new InspectionService(cleanUrl, _configService.InspectionDefinitions);
				InspectionData dnsResult = inspection.Get();

				DistributedCacheEntryOptions cacheOptions = new DistributedCacheEntryOptions().SetAbsoluteExpiration(TimeSpan.FromMinutes(10));
				await _cache.SetStringAsync(key, JsonConvert.SerializeObject(dnsResult), cacheOptions);

				return new JsonResult(dnsResult);
			}
			catch (AggregateException ex)
			{
				return StatusCode(StatusCodes.Status503ServiceUnavailable, ex.Message);
			}
		}
	}
}
