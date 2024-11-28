using System.Net.Http.Headers;
using System.Text.RegularExpressions;
using HtmlAgilityPack;
using Whatsthis.API.Models;

namespace Whatsthis.API.Service
{
	public interface IInspectionService
	{
		InspectionData Get();
		List<InspectionResultInformation> DetectAll(List<InspectionEntity> entity);
		(int[], List<string>) CountBodyReferences(List<string> xpathExpressions);
		(int[], List<string>) CountHeaderReferences(List<string> headers);
	}

	public class InspectionService : IInspectionService
	{
		private readonly string _url;
		private readonly InspectionSetup _inspectionDefs;
		private HtmlDocument _websiteBody = new HtmlDocument();
		private HttpResponseHeaders? _websiteHeaders;

		public InspectionService(string url, InspectionSetup inspectionDefs)
		{
			_url = url;
			_inspectionDefs = inspectionDefs;
			ParseInputUrl();
		}

		public InspectionData Get()
		{
			InspectionData parsed = new InspectionData();
			parsed.URL = _url;
			parsed.Technology.cms = DetectAll(_inspectionDefs.cms);
			parsed.Technology.frontend = DetectAll(_inspectionDefs.frontend);
			parsed.Technology.javascript = DetectAll(_inspectionDefs.javascript);
			parsed.Technology.seo = DetectAll(_inspectionDefs.seo);
			parsed.Technology.cdn = DetectAll(_inspectionDefs.cdn);
			parsed.Technology.language = DetectAll(_inspectionDefs.language);
			parsed.Technology.server = DetectAll(_inspectionDefs.server);

			return parsed;
		}

		public List<InspectionResultInformation> DetectAll(List<InspectionEntity> entity)
		{
			List<InspectionResultInformation> inspectList = new List<InspectionResultInformation>();

			foreach (InspectionEntity inspection in entity)
			{
				(int[], List<string>) matchedBody = CountBodyReferences(inspection.body);
				(int[], List<string>) matchedHeader = CountHeaderReferences(inspection.headers);
				int totalMatch = matchedBody.Item1.Sum() + matchedHeader.Item1.Sum();

				if (totalMatch > 0)
				{
					List<string> combinedMatches = new List<string>();
					combinedMatches.AddRange(matchedBody.Item2);
					combinedMatches.AddRange(matchedHeader.Item2);

					InspectionResultInformation detection = new InspectionResultInformation();
					detection.Name = inspection.name;
					detection.Description = inspection.description;
					detection.URL = inspection.url;
					detection.MatchAvailable = combinedMatches.Count();
					detection.MatchedOn = combinedMatches;

					inspectList.Add(detection);
				}
			}

			return inspectList;
		}

		public (int[], List<string>) CountBodyReferences(List<string> xpathExpressions)
		{
			int[] hitCounts = new int[xpathExpressions.Count];
			List<string> matchedExpressions = new List<string>();

			for (int i = 0; i < xpathExpressions.Count; i++)
			{
				HtmlNodeCollection nodes = _websiteBody.DocumentNode.SelectNodes(xpathExpressions[i]);
				if (nodes != null && nodes.Count > 0)
				{
					hitCounts[i] = nodes.Count;
					matchedExpressions.Add(xpathExpressions[i]);
				}
			}

			return (hitCounts, matchedExpressions);
		}

		public (int[], List<string>) CountHeaderReferences(List<string> headers)
		{
			int[] hitCounts = new int[headers.Count];
			List<string> matchedHeaders = new List<string>();

			foreach (string header in headers)
			{
				string[] headerParts = header.Split(':');
				if (headerParts.Length == 2)
				{
					string headerName = headerParts[0].Trim();
					string headerValue = headerParts[1].Trim();

					IEnumerable<string>? values;
					if (_websiteHeaders?.TryGetValues(headerName, out values) ?? false)
					{
						Regex regex = new Regex(headerValue);
						foreach (string value in values)
						{
							if (regex.IsMatch(value))
							{
								hitCounts[headers.IndexOf(header)]++;
								matchedHeaders.Add(header);
							}
						}
					}
				}
			}

			return (hitCounts, matchedHeaders);
		}

		private void ParseInputUrl()
		{
			using (HttpClient client = new HttpClient())
			{
				client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0");
				HttpResponseMessage response = client.GetAsync(_url).Result;
				response.EnsureSuccessStatusCode();
				string responseContent = response.Content.ReadAsStringAsync().Result;
				_websiteHeaders = response.Headers;
				_websiteBody.LoadHtml(responseContent);
			}
		}
	}
}
