namespace WhatsthisAPI.Models
{
	public class InspectionData
	{
		public string? URL { get; set; }
		public InspectionTechnologyCollection Technology { get; set; } = new InspectionTechnologyCollection();
	}
}
