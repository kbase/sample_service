
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
 * <p>Original spec-file type: GetSamplesParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "samples",
    "as_admin"
})
public class GetSamplesParams {

    @JsonProperty("samples")
    private List<SampleIdentifier> samples;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("samples")
    public List<SampleIdentifier> getSamples() {
        return samples;
    }

    @JsonProperty("samples")
    public void setSamples(List<SampleIdentifier> samples) {
        this.samples = samples;
    }

    public GetSamplesParams withSamples(List<SampleIdentifier> samples) {
        this.samples = samples;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public GetSamplesParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
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
        return ((((((("GetSamplesParams"+" [samples=")+ samples)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
