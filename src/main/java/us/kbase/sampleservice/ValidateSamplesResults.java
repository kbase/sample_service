
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
 * <p>Original spec-file type: ValidateSamplesResults</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "errors"
})
public class ValidateSamplesResults {

    @JsonProperty("errors")
    private List<ValidateSamplesError> errors;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("errors")
    public List<ValidateSamplesError> getErrors() {
        return errors;
    }

    @JsonProperty("errors")
    public void setErrors(List<ValidateSamplesError> errors) {
        this.errors = errors;
    }

    public ValidateSamplesResults withErrors(List<ValidateSamplesError> errors) {
        this.errors = errors;
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
        return ((((("ValidateSamplesResults"+" [errors=")+ errors)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
