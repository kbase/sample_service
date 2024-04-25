
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
 * <p>Original spec-file type: GetDataLinksFromDataResults</p>
 * <pre>
 * get_data_links_from_data results.
 *         links - the links.
 *         effective_time - the time at which the query was run. This timestamp, if saved, can be
 *             used when running the method again to ensure reproducible results.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "links",
    "effective_time"
})
public class GetDataLinksFromDataResults {

    @JsonProperty("links")
    private List<DataLink> links;
    @JsonProperty("effective_time")
    private Long effectiveTime;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("links")
    public List<DataLink> getLinks() {
        return links;
    }

    @JsonProperty("links")
    public void setLinks(List<DataLink> links) {
        this.links = links;
    }

    public GetDataLinksFromDataResults withLinks(List<DataLink> links) {
        this.links = links;
        return this;
    }

    @JsonProperty("effective_time")
    public Long getEffectiveTime() {
        return effectiveTime;
    }

    @JsonProperty("effective_time")
    public void setEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public GetDataLinksFromDataResults withEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
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
        return ((((((("GetDataLinksFromDataResults"+" [links=")+ links)+", effectiveTime=")+ effectiveTime)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
