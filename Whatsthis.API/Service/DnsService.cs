using Whatsthis.API.Models;
using DnsClient;
using DnsClient.Protocol;

namespace Whatsthis.API.Service
{
	public interface IDnsService
	{
		DnsData Get(string url);
	}

	public class DnsService : IDnsService
	{
		public DnsData Get(string url)
		{
			DnsData parsed = new DnsData();

			LookupClient client = new LookupClient();
			List<QueryType> queryTypes = new List<QueryType> {
				QueryType.A,
				QueryType.AAAA,
				QueryType.CNAME,
				QueryType.MX,
				QueryType.TXT,
				QueryType.NS
			};
			foreach (QueryType queryType in queryTypes)
			{
				IDnsQueryResponse? result = client.Query(url, queryType);

				foreach (DnsClient.Protocol.DnsResourceRecord answer in result.Answers)
				{
					switch (answer.RecordType)
					{
						case ResourceRecordType.A:
							if (answer is ARecord aRecord)
							{
								parsed.A.Add(aRecord.Address.ToString());
							}
							break;
						case ResourceRecordType.AAAA:
							if (answer is AaaaRecord aaaaRecord)
							{
								parsed.AAAA.Add(aaaaRecord.Address.ToString());
							}
							break;
						case ResourceRecordType.CNAME:
							if (answer is CNameRecord cnameRecord)
							{
								parsed.CNAME.Add(cnameRecord.DomainName.ToString());
							}
							break;
						case ResourceRecordType.NS:
							if (answer is NsRecord nsRecord)
							{
								parsed.NS.Add(nsRecord.DomainName.ToString());
							}
							break;
						case ResourceRecordType.MX:
							if (answer is MxRecord mxRecord)
							{
								DnsMailData mailData = new DnsMailData();
								mailData.Address = mxRecord.DomainName.ToString();
								mailData.Priority = mxRecord.Preference;
								parsed.MX.Add(mailData);
							}
							break;
						case ResourceRecordType.TXT:
							if (answer is TxtRecord txtRecord)
							{
								parsed.TXT.Add(string.Join("", txtRecord.Text));
							}
							break;
					}
				}
			}

			return parsed;
		}
	}
}
