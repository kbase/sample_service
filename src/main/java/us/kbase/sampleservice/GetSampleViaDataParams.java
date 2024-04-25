
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
 * <p>Original spec-file type: GetSampleViaDataParams</p>
 * <pre>
 * get_sample_via_data parameters.
 *         upa - the workspace UPA of the target object.
 *         id - the target sample id.
 *         version - the target sample version.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "upa",
    "id",
    "version"
})
public class GetSampleViaDataParams {

    @JsonProperty("upa")
    private String upa;
    @JsonProperty("id")
    private String id;
    @JsonProperty("version")
    private Long version;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("upa")
    public String getUpa() {
        return upa;
    }

    @JsonProperty("upa")
    public void setUpa(String upa) {
        this.upa = upa;
    }

    public GetSampleViaDataParams withUpa(String upa) {
        this.upa = upa;
        return this;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public GetSampleViaDataParams withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public GetSampleViaDataParams withVersion(Long version) {
        this.version = version;
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
        return ((((((((("GetSampleViaDataParams"+" [upa=")+ upa)+", id=")+ id)+", version=")+ version)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
