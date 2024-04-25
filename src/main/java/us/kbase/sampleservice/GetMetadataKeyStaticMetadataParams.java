
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
 * <p>Original spec-file type: GetMetadataKeyStaticMetadataParams</p>
 * <pre>
 * get_metadata_key_static_metadata parameters.
 *         keys - the list of metadata keys to interrogate.
 *         prefix -
 *             0 (the default) to interrogate standard metadata keys.
 *             1 to interrogate prefix metadata keys, but require an exact match to the prefix key.
 *             2 to interrogate prefix metadata keys, but any keys which are a prefix of the
 *                 provided keys will be included in the results.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "keys",
    "prefix"
})
public class GetMetadataKeyStaticMetadataParams {

    @JsonProperty("keys")
    private List<String> keys;
    @JsonProperty("prefix")
    private Long prefix;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("keys")
    public List<String> getKeys() {
        return keys;
    }

    @JsonProperty("keys")
    public void setKeys(List<String> keys) {
        this.keys = keys;
    }

    public GetMetadataKeyStaticMetadataParams withKeys(List<String> keys) {
        this.keys = keys;
        return this;
    }

    @JsonProperty("prefix")
    public Long getPrefix() {
        return prefix;
    }

    @JsonProperty("prefix")
    public void setPrefix(Long prefix) {
        this.prefix = prefix;
    }

    public GetMetadataKeyStaticMetadataParams withPrefix(Long prefix) {
        this.prefix = prefix;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((("GetMetadataKeyStaticMetadataParams"+" [keys=")+ keys)+", prefix=")+ prefix)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
