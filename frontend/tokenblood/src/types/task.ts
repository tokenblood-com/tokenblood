export interface TaskConfiguration {
  number: number
  name: string
  backend_name: string
  description: string
}

export const getTask = async (taskName: string): Promise<TaskConfiguration> => {
  // Mock implementation
  return {
    number: 1,
    name: "Personal Information Extraction",
    backend_name: "personal_info_extraction_debug",
    description: `Documents contain references to individuals by name. Your task is to write a prompt that accurately extracts all full personal names from the text and returns them as a single string, where persons are separated with comma.

Example output: 
“Jack Blue, Andrew Green, May Davidson" 

Note:
- Some names may contain typos. In your response, you should not correct them.`
  }
} 