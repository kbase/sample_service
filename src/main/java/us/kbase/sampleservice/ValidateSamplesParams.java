
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
 * <p>Original spec-file type: ValidateSamplesParams</p>
 * <pre>
 * Provide sample and run through the validation steps, but without saving them. Allows all the samples to be evaluated for validity first so potential errors can be addressed.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "samples"
})
public class ValidateSamplesParams {

    @JsonProperty("samples")
    private List<Sample> samples;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("samples")
    public List<Sample> getSamples() {
        return samples;
    }

    @JsonProperty("samples")
    public void setSamples(List<Sample> samples) {
        this.samples = samples;
    }

    public ValidateSamplesParams withSamples(List<Sample> samples) {
        this.samples = samples;
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
        return ((((("ValidateSamplesParams"+" [samples=")+ samples)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
