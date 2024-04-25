
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GetDataLinkParams</p>
 * <pre>
 * get_data_link parameters.
 *         linkid - the link ID.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "linkid"
})
public class GetDataLinkParams {

    @JsonProperty("linkid")
    private String linkid;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("linkid")
    public String getLinkid() {
        return linkid;
    }

    @JsonProperty("linkid")
    public void setLinkid(String linkid) {
        this.linkid = linkid;
    }

    public GetDataLinkParams withLinkid(String linkid) {
        this.linkid = linkid;
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
        return ((((("GetDataLinkParams"+" [linkid=")+ linkid)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
