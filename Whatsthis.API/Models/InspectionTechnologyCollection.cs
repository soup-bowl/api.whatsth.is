namespace Whatsthis.API.Models
{
	public class InspectionTechnologyCollection
	{
		public List<InspectionResultInformation> cms { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> frontend { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> javascript { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> seo { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> cdn { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> language { get; set; } = new List<InspectionResultInformation>();
		public List<InspectionResultInformation> server { get; set; } = new List<InspectionResultInformation>();
	}
}
