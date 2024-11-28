namespace Whatsthis.API.Models
{
	public class InspectionSetup
	{
		public List<InspectionEntity> cms { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> frontend { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> javascript { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> seo { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> cdn { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> language { get; set; } = new List<InspectionEntity>();
		public List<InspectionEntity> server { get; set; } = new List<InspectionEntity>();
	}
}
