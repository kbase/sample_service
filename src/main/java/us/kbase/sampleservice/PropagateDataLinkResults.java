
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: PropagateDataLinkResults</p>
 * <pre>
 * propagate_data_links results.
 *         links - the links.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "links"
})
public class PropagateDataLinkResults {

    @JsonProperty("links")
    private List<DataLink> links;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("links")
    public List<DataLink> getLinks() {
        return links;
    }

    @JsonProperty("links")
    public void setLinks(List<DataLink> links) {
        this.links = links;
    }

    public PropagateDataLinkResults withLinks(List<DataLink> links) {
        this.links = links;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("PropagateDataLinkResults"+" [links=")+ links)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
