using System.Text.RegularExpressions;
using System.Globalization;
using Whatsthis.API.Models;
using Whois.NET;

namespace Whatsthis.API.Service
{
	public interface IWhoisService
	{
		WhoisData? Get(string url);
	}

	public class WhoisService : IWhoisService
	{
		public WhoisData? Get(string url)
		{
			WhoisResponse result = WhoisClient.Query(url);
			if (result.OrganizationName != null)
			{
				return ParseWhoisData(result.Raw);
			}
			return null;
		}

		private WhoisData ParseWhoisData(string whois)
		{
			WhoisData whodata = new WhoisData();
			whodata.Domain = GetMatch(whois, @"Domain Name:\s+(.+)");
			whodata.Whois = GetMatch(whois, @"WHOIS Server:\s+(.+)");
			whodata.Registrar = GetMatch(whois, @"Registrar:\s+(.+)");
			whodata.Created = ParseDate(GetMatch(whois, @"Creation Date:\s+(.+)"));
			whodata.Updated = ParseDate(GetMatch(whois, @"Updated Date:\s+(.+)"));
			whodata.Expires = ParseDate(GetMatch(whois, @"Expir\w+ Date:\s+(.+)"));
			whodata.NameServers = GetMultiMatch(whois, @"Name Server:\s+(.+?)\n");

			return whodata;
		}

		private DateTime? ParseDate(string input)
		{
			DateTime dateOutput;
			string[] formats =  {
				"dd-MMM-yyyy",                // 02-jan-2000
				"dd-MMMM-yyyy",               // 11-February-2000
				"dd-MM-yyyy",                 // 20-10-2000
				"yyyy-MM-dd",                 // 2000-01-02
				"d.M.yyyy",                   // 2.1.2000
				"yyyy.M.d",                   // 2000.01.02
				"yyyy/MM/dd",                 // 2000/01/02
				"yyyy/MM/dd HH:mm:ss",        // 2011/06/01 01:05:01
				"yyyy/MM/dd HH:mm:ss (zzz)",  // 2011/06/01 01:05:01 (+0900)
				"yyyyMMdd",                   // 20170209
				"yyyyMMdd HH:mm:ss",          // 20110908 14:44:51
				"dd/MM/yyyy",                 // 02/01/2013
				"yyyy. MM. dd.",              // 2000. 01. 02.
				"yyyy.MM.dd HH:mm:ss",        // 2014.03.08 10:28:24
				"dd-MMM-yyyy HH:mm:ss zzz",   // 24-Jul-2009 13:20:03 UTC
				"ddd MMM dd HH:mm:ss zzz yyyy",  // Tue Jun 21 23:59:59 GMT 2011
				"ddd MMM dd yyyy",            // Tue Dec 12 2000
				"yyyy-MM-ddTHH:mm:ss",        // 2007-01-26T19:10:31
				"yyyy-MM-ddTHH:mm:ssZ",       // 2007-01-26T19:10:31Z
				"yyyy-MM-ddTHH:mm:ssZ'['zzz']'",   // 2007-01-26T19:10:31Z[UTC]
				"yyyy-MM-ddTHH:mm:ss.fffZ",    // 2018-12-01T16:17:30.568Z
				"yyyy-MM-ddTHH:mm:ss.fffzzz",  // 2011-09-08T14:44:51.622265+03:00
				"yyyy-MM-ddTHH:mm:sszzz",      // 2013-12-06T08:17:22-0800
				"yyyy-MM-ddTHH:mm:sszzzZ",     // 1970-01-01T02:00:00+02:00Z
				"yyyy-MM-dd't'HH:mm:ss.fff",   // 2011-09-08t14:44:51.622265
				"yyyy-MM-dd't'HH:mm:ss",       // 2007-01-26T19:10:31
				"yyyy-MM-dd't'HH:mm:ssZ",      // 2007-01-26T19:10:31Z
				"yyyy-MM-dd't'HH:mm:ss.fffZ",  // 2007-01-26t19:10:31.00z
				"yyyy-MM-dd't'HH:mm:sszzz",    // 2011-03-30T19:36:27+0200
				"yyyy-MM-dd't'HH:mm:ss.fffzzz", // 2011-09-08T14:44:51.622265+03:00
				"yyyy-MM-dd HH:mm:ssZ",       // 2000-08-22 18:55:20Z
				"yyyy-MM-dd HH:mm:ss",        // 2000-08-22 18:55:20
				"dd MMM yyyy HH:mm:ss",       // 08 Apr 2013 05:44:00
				"dd/MM/yyyy HH:mm:ss",        // 23/04/2015 12:00:07 EEST
				"dd/MM/yyyy HH:mm:ss zzz",    // 23/04/2015 12:00:07 EEST
				"dd/MM/yyyy HH:mm:ss.ffffff zzz",  // 23/04/2015 12:00:07.619546 EEST
				"MMMM dd yyyy",               // August 14 2017
				"dd.MM.yyyy HH:mm:ss",        // 08.03.2014 10:28:24
				"'before' MMM-yyyy",           // before aug-1996
				"yyyy-MM-dd HH:mm:ss (zzzzz)" // 2017-09-26 11:38:29 (GMT+00:00)
			};

			if (DateTime.TryParseExact(input, formats, CultureInfo.InvariantCulture, DateTimeStyles.None, out dateOutput))
			{
				return dateOutput;
			}
			else
			{
				return null;
			}
		}

		private string GetMatch(string input, string pattern)
		{
			Match match = Regex.Match(input, pattern, RegexOptions.IgnoreCase);
			if (match.Success)
			{
				return match.Groups[1].Value.Replace("\r", "").Replace("\n", "").Trim();
			}
			else
			{
				return "";
			}
		}

		private List<string> GetMultiMatch(string input, string pattern)
		{
			List<string> matchList = new List<string>();
			MatchCollection matches = Regex.Matches(input, pattern, RegexOptions.IgnoreCase);
			foreach (Match match in matches)
			{
				string matchItemContent = match.Groups[1].Value.Trim();
				matchList.Add(matchItemContent);
			}
			return matchList;
		}
	}
}
