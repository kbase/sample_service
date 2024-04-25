
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
 * <p>Original spec-file type: ValidateSamplesError</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "message",
    "dev_message",
    "sample_name",
    "node",
    "key",
    "subkey"
})
public class ValidateSamplesError {

    @JsonProperty("message")
    private String message;
    @JsonProperty("dev_message")
    private String devMessage;
    @JsonProperty("sample_name")
    private String sampleName;
    @JsonProperty("node")
    private String node;
    @JsonProperty("key")
    private String key;
    @JsonProperty("subkey")
    private String subkey;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("message")
    public String getMessage() {
        return message;
    }

    @JsonProperty("message")
    public void setMessage(String message) {
        this.message = message;
    }

    public ValidateSamplesError withMessage(String message) {
        this.message = message;
        return this;
    }

    @JsonProperty("dev_message")
    public String getDevMessage() {
        return devMessage;
    }

    @JsonProperty("dev_message")
    public void setDevMessage(String devMessage) {
        this.devMessage = devMessage;
    }

    public ValidateSamplesError withDevMessage(String devMessage) {
        this.devMessage = devMessage;
        return this;
    }

    @JsonProperty("sample_name")
    public String getSampleName() {
        return sampleName;
    }

    @JsonProperty("sample_name")
    public void setSampleName(String sampleName) {
        this.sampleName = sampleName;
    }

    public ValidateSamplesError withSampleName(String sampleName) {
        this.sampleName = sampleName;
        return this;
    }

    @JsonProperty("node")
    public String getNode() {
        return node;
    }

    @JsonProperty("node")
    public void setNode(String node) {
        this.node = node;
    }

    public ValidateSamplesError withNode(String node) {
        this.node = node;
        return this;
    }

    @JsonProperty("key")
    public String getKey() {
        return key;
    }

    @JsonProperty("key")
    public void setKey(String key) {
        this.key = key;
    }

    public ValidateSamplesError withKey(String key) {
        this.key = key;
        return this;
    }

    @JsonProperty("subkey")
    public String getSubkey() {
        return subkey;
    }

    @JsonProperty("subkey")
    public void setSubkey(String subkey) {
        this.subkey = subkey;
    }

    public ValidateSamplesError withSubkey(String subkey) {
        this.subkey = subkey;
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
        return ((((((((((((((("ValidateSamplesError"+" [message=")+ message)+", devMessage=")+ devMessage)+", sampleName=")+ sampleName)+", node=")+ node)+", key=")+ key)+", subkey=")+ subkey)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
