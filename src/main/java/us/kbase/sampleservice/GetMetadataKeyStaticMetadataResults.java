
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: GetMetadataKeyStaticMetadataResults</p>
 * <pre>
 * get_metadata_key_static_metadata results.
 *         static_metadata - the static metadata for the requested keys.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "static_metadata"
})
public class GetMetadataKeyStaticMetadataResults {

    @JsonProperty("static_metadata")
    private Map<String, Map<String, UObject>> staticMetadata;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("static_metadata")
    public Map<String, Map<String, UObject>> getStaticMetadata() {
        return staticMetadata;
    }

    @JsonProperty("static_metadata")
    public void setStaticMetadata(Map<String, Map<String, UObject>> staticMetadata) {
        this.staticMetadata = staticMetadata;
    }

    public GetMetadataKeyStaticMetadataResults withStaticMetadata(Map<String, Map<String, UObject>> staticMetadata) {
        this.staticMetadata = staticMetadata;
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
        return ((((("GetMetadataKeyStaticMetadataResults"+" [staticMetadata=")+ staticMetadata)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
