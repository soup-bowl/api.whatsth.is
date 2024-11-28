using System.Net;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using Whatsthis.API.Models;
using Whatsthis.API.Service;
using Microsoft.Extensions.Caching.Distributed;
using Newtonsoft.Json;
using Whatsthis.API.Utilities;

namespace Whatsthis.API.Controllers
{
	[ApiController]
	[Route("/")]
	public class DomainController(IDistributedCache cache) : ControllerBase
	{
		private readonly IDistributedCache _cache = cache;

        /// <summary>
        /// Whois Lookup
        /// </summary>
        /// <remarks>
        /// Performs a WHOIS lookup on the URL specified. This helps to ascertain ownership information at a high level.
        ///
        /// For more info, see: https://en.wikipedia.org/wiki/WHOIS
        ///
        /// This does not aim to provide full WHOIS information. This is due to the rise of WHOIS information
        /// protection, the contact-level information is no longer useful. Instead this provides info such as
        /// registration and expiration dates, and registrar used.
        /// </remarks>
        [HttpGet("whois/{url}")]
		[ProducesResponseType(typeof(WhoisData), StatusCodes.Status200OK)]
		[ProducesResponseType(typeof(string), StatusCodes.Status503ServiceUnavailable)]
		public async Task<ActionResult<string>> WhoisLookup(string url)
		{
			string decodedUrl = WebUtility.UrlDecode(url);
			string cleanUrl = UrlHelper.CleanUrl(decodedUrl);
			string key = $"whois-{cleanUrl}";

			string? cachedData = await _cache.GetStringAsync(key);

			if (cachedData != null)
			{
				WhoisData data = JsonConvert.DeserializeObject<WhoisData>(cachedData)!;
				return new JsonResult(data);
			}
			else
			{
				WhoisService whois = new();
				WhoisData? response = whois.Get(cleanUrl);

				if (response != null)
				{
					DistributedCacheEntryOptions cacheOptions = new DistributedCacheEntryOptions().SetAbsoluteExpiration(TimeSpan.FromMinutes(10)); // cache for 10 minutes
					await _cache.SetStringAsync(key, JsonConvert.SerializeObject(response), cacheOptions);

					return new JsonResult(response);
				}
				else
				{
					return StatusCode(StatusCodes.Status503ServiceUnavailable, "Could not find data on this domain. Either the input is invalid, or the TLD is not currently supported.");
				}
			}
		}

		/// <summary>
		/// Dns Lookup
		/// </summary>
		/// <remarks>
		/// This endpoint checks all the common DNS endpoints for records against the input URL.
		/// </remarks>
		[HttpGet("dns/{url}")]
		[ProducesResponseType(typeof(DnsData), StatusCodes.Status200OK)]
		public async Task<ActionResult<string>> DomainLookup(string url)
		{
			string decodedUrl = WebUtility.UrlDecode(url);
			string cleanUrl = UrlHelper.CleanUrl(decodedUrl);
			string key = $"dns-{cleanUrl}";

			string? cachedData = await _cache.GetStringAsync(key);

			if (cachedData != null)
			{
				DnsData data = JsonConvert.DeserializeObject<DnsData>(cachedData)!;
				return new JsonResult(data);
			}
			else
			{
				DnsService dns = new();
				DnsData response = dns.Get(cleanUrl);

				if (response != null)
				{
					DistributedCacheEntryOptions cacheOptions = new DistributedCacheEntryOptions().SetAbsoluteExpiration(TimeSpan.FromMinutes(10)); // cache for 10 minutes
					await _cache.SetStringAsync(key, JsonConvert.SerializeObject(response), cacheOptions);

					return new JsonResult(response);
				}
				else
				{
					return StatusCode(StatusCodes.Status503ServiceUnavailable, "Could not find data on this domain. Either the input is invalid, or the TLD is not currently supported.");
				}
			}
		}
	}
}
